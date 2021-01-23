import sys
from dataclasses import dataclass, fields
from typing import Tuple

from wired import ServiceContainer
from wired_injector.pipeline import (
    FieldInfo,
    Pipeline,
    Result,
)
from wired_injector.pipeline.field_info import dataclass_field_info_factory
from wired_injector.pipeline.results import (
    Init,
    Found,
    Skip,
)
from wired_injector.pipeline.rules import (
    AnnotationPipeline,
    IsContainer,
    IsInProps,
    IsInit,
    IsSimpleType,
)

from .conftest import DummyTarget

if sys.version_info[:3] >= (3, 9):
    from typing import get_type_hints
else:  # pragma: no cover
    from typing_extensions import get_type_hints


def test_default_field_info(dummy_title_field: FieldInfo) -> None:
    # Ensure it meets the protocol
    meets_protocol: FieldInfo = dummy_title_field
    assert meets_protocol

    dfi = dummy_title_field
    assert dfi.field_name == 'title'
    assert False is dfi.has_annotated


def test_is_init_false(
    dummy_title_field: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # FieldIsInit rule on a field with init=False
    dummy_title_field.init = False
    field_is_init = IsInit(dummy_title_field, dummy_pipeline)
    result: Result = field_is_init()
    assert isinstance(result, Init)
    assert str == result.value


def test_is_init_true(
    dummy_title_field: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # FieldIsInit rule on a field with init=True
    dummy_title_field.init = True
    field_is_init = IsInit(dummy_title_field, dummy_pipeline)
    result: Result = field_is_init()
    assert isinstance(result, Skip)
    assert str == result.value


def test_is_in_props_no_props(
    dummy_title_field: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # No props
    field_is_props = IsInProps(dummy_title_field, dummy_pipeline)
    result: Result = field_is_props()
    assert isinstance(result, Skip)
    assert str == result.value


def test_is_in_props_not_in(
    dummy_title_field: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # There are props, but the field_name 'foo' isn't in it
    dummy_pipeline.props = dict(nottitle=1)
    field_is_props = IsInProps(dummy_title_field, dummy_pipeline)
    result: Result = field_is_props()
    assert isinstance(result, Skip)
    assert str == result.value


def test_is_in_props_in_props(
    dummy_title_field: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # There are props passed in and the field_value is in it
    dummy_pipeline.props = dict(title='In Props')
    field_is_props = IsInProps(dummy_title_field, dummy_pipeline)
    result: Result = field_is_props()
    assert isinstance(result, Found)
    assert 'In Props' == result.value


def test_is_in_system_props_no_system_props(
    dummy_title_field: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # No system props
    dummy_pipeline.props = {}
    dummy_pipeline.system_props = {}
    field_is_props = IsInProps(dummy_title_field, dummy_pipeline)
    result: Result = field_is_props()
    assert isinstance(result, Skip)
    assert str == result.value


def test_is_in_system_props_not_in(
    dummy_title_field: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # There are system props, but the field_name 'foo' isn't in it
    dummy_pipeline.props = {}
    dummy_pipeline.system_props = dict(notfoo=1)
    field_is_props = IsInProps(dummy_title_field, dummy_pipeline)
    result: Result = field_is_props()
    assert isinstance(result, Skip)
    assert str == result.value


def test_is_in_system_props_in_props(
    dummy_title_field: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # There are system props passed in and the field_value is in it
    dummy_pipeline.props = {}
    dummy_pipeline.system_props = dict(title='In System Props')
    field_is_props = IsInProps(dummy_title_field, dummy_pipeline)
    result: Result = field_is_props()
    assert isinstance(result, Found)
    assert 'In System Props' == result.value


def test_is_in_both_props_and_system_props(
    dummy_title_field: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # Props has higher precedence than system props
    dummy_pipeline.props = dict(title='In Props')
    dummy_pipeline.system_props = dict(title='In System Props')
    field_is_props = IsInProps(dummy_title_field, dummy_pipeline)
    result: Result = field_is_props()
    assert isinstance(result, Found)
    assert 'In Props' == result.value


def test_is_not_container(
    dummy_title_field: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # The field is NOT asking for field_type=ServiceContainer
    field_is_container = IsContainer(dummy_title_field, dummy_pipeline)
    result: Result = field_is_container()
    assert isinstance(result, Skip)
    assert str == result.value


def test_is_container(
    dummy_title_field: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    dummy_title_field.field_type = ServiceContainer
    field_is_container = IsContainer(dummy_title_field, dummy_pipeline)
    result: Result = field_is_container()
    assert isinstance(result, Found)
    assert dummy_pipeline.container == result.value


def test_is_simple_type(
    dummy_title_field: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    fake_lookups = getattr(dummy_pipeline.container, 'fake_lookups')
    dt = DummyTarget(age=99)
    fake_lookups[DummyTarget] = dt
    dummy_title_field.field_type = DummyTarget
    field_is_simple_type = IsSimpleType(dummy_title_field, dummy_pipeline)
    result: Result = field_is_simple_type()
    assert isinstance(result, Found)
    assert result.value == dt


def test_is_simple_type_builtin(
    dummy_title_field: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # No pipeline but looking up a type that is built-in and
    # trying to look it up causes a TypeError in wired, e.g.
    # customer_name: str = 'Customer Name'  # noqa: E800
    dummy_title_field.field_type = str
    dummy_title_field.default_value = 'yes'
    field_is_simple_type = IsSimpleType(dummy_title_field, dummy_pipeline)
    result: Result = field_is_simple_type()
    assert isinstance(result, Skip)
    assert result.value == IsSimpleType


def test_is_simple_type_generic(
    dummy_pipeline: Pipeline,
) -> None:
    # No pipeline but looking up a type that is wrapped
    # in a generic such as Tuple[str, ...]
    @dataclass
    class DummyGenericField:
        titles: Tuple[str, ...] = ('first', 'second')

    # Get the field info
    type_hints = get_type_hints(DummyGenericField, include_extras=True)
    fields_mapping = {f.name: f for f in fields(DummyGenericField)}
    field_infos = [
        dataclass_field_info_factory(fields_mapping[field_name])
        for field_name in type_hints
    ]
    field_info = field_infos[0]

    field_is_simple_type = IsSimpleType(field_info, dummy_pipeline)
    result: Result = field_is_simple_type()
    assert isinstance(result, Skip)
    assert result.value == IsSimpleType


def test_is_not_simple_type(
    dummy_annotated_field: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # This has a field with annotated type, so the rule doesn't match,
    # and instead it skips.
    field_is_not_simple_type = IsSimpleType(
        dummy_annotated_field, dummy_pipeline
    )
    result: Result = field_is_not_simple_type()
    assert isinstance(result, Skip)
    assert IsSimpleType == result.value


def test_annotation_pipeline_no_operators(
    dummy_title_field: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # Doing Annotated but there aren't any operators, so Skip
    # to allow default to do something.
    dummy_title_field.operators = tuple()
    field_is_container = AnnotationPipeline(dummy_title_field, dummy_pipeline)
    result: Result = field_is_container()
    assert isinstance(result, Skip)
