from dataclasses import dataclass
from typing import NamedTuple, Tuple, Optional, Callable

import pytest
from wired_injector.injector import SkipField
from wired_injector.operators import (
    Context,
    Field, Operator,
)
from wired_injector.pipeline import Pipeline
from wired_injector.pipeline2.rules import DefaultFieldInfo


@dataclass
class Target:
    name: str = 'Some Target'


def make_pipeline(
    regular_container,
    operators: Tuple['Operator', ...],
    target: Optional[Callable] = Target,
) -> Pipeline:
    field_info = DefaultFieldInfo(
        field_name='title',
        field_type=str,
        default_value=None,
        init=False,
        operators=operators,
    )
    pipeline = Pipeline(
        field_info=field_info,
        container=regular_container,
        target=target,
    )
    return pipeline

#
# def test_get(regular_container):
#     get = Get(View)
#     pipeline = make_pipeline(regular_container, (get,))
#     result: View = get(None, pipeline)
#     assert result.name == 'View'
#
#
# def test_get_injectable_attr(regular_container):
#     get = Get(Greeting)
#     pipeline = make_pipeline(regular_container, (get,))
#     result: Greeting = get(None, pipeline)
#     assert result() == 'Hello VIEW'
#
#
# def test_get_attr(regular_container):
#     get = Get(View, attr='name')
#     pipeline = make_pipeline(regular_container, (get,))
#     result: View = get(None, pipeline)
#     assert result == 'View'
#
#
# def test_get_failed(regular_container):
#     class NotFound:
#         pass
#
#     pipeline = make_pipeline(regular_container, tuple())
#     with pytest.raises(SkipField):
#         Get(NotFound)(None, pipeline)
#
#
# def test_attr(regular_container):
#     attr = Attr('name')
#     pipeline = make_pipeline(regular_container, (attr,))
#     previous = Customer()
#     result = attr(previous, pipeline)
#     assert 'Customer' == result
#
#
# def test_get_then_attr(regular_container):
#     get = Get(View)
#     pipeline = make_pipeline(regular_container, (get,))
#     result1 = get(None, pipeline)
#     attr = Attr('name')
#     result = attr(result1, pipeline)
#     assert 'View' == result


def test_context_attr(regular_container):
    context = Context(attr='name')
    pipeline = make_pipeline(regular_container, (context,))
    result = context(None, pipeline)
    assert result == 'Customer'


def test_context_none_attr(regular_container):
    regular_container.context = None
    context = Context(attr='name')
    pipeline = make_pipeline(regular_container, (context,))
    with pytest.raises(SkipField):
        context(None, pipeline)


def test_field_target_is_dataclass(regular_container):
    field = Field('name')
    operators = (field,)
    pipeline = make_pipeline(regular_container, (field,))
    result = field(None, pipeline)
    assert result == 'Some Target'


def test_field_target_is_named_tuple(regular_container):
    class TupleTarget(NamedTuple):
        name: str = 'Some TupleTarget'

    field = Field('name')
    pipeline = make_pipeline(regular_container, (field,),
                             target=TupleTarget)
    result = field(None, pipeline)
    assert result == 'Some TupleTarget'


def test_field_target_is_function(regular_container):
    def FunctionTarget(name: str = 'Some FunctionTarget'):
        return

    field = Field('name')
    pipeline = make_pipeline(
        regular_container, (field,),
        target=FunctionTarget,
    )
    result = field(None, pipeline)
    assert result == 'Some FunctionTarget'


def test_field_target_missing_field(regular_container):
    field = Field('bogus')
    pipeline = make_pipeline(regular_container, (field,))
    with pytest.raises(KeyError) as exc:
        field(None, pipeline)
    assert str(exc.value.args[0]) == 'No field "bogus" on target "Target"'
