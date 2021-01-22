from typing import Dict, Any

from wired import ServiceContainer
from wired_injector.pipeline2 import (
    FieldInfo,
    Pipeline,
    Result,
)
from wired_injector.pipeline2.results import Init, Skip, Found, Error
from wired_injector.pipeline2.rules import (
    AnnotationPipeline,
    IsContainer,
    IsInProps,
    IsInit,
    IsSimpleType,
)

from .conftest import DummyTarget

def test_default_field_info(dummy_title_field: FieldInfo) -> None:
    # Ensure it meets the protocol
    meets_protocol: FieldInfo = dummy_title_field
    assert meets_protocol

    dfi = dummy_title_field
    assert dfi.field_name == 'title'


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
    props: Dict[Any, Any] = {}
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


def test_is_not_simple_type(
    dummy_annotated_field: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # This has a field with annotated type, so the rule doesn't match,
    # and instead it skips.
    field_is_not_simple_type = IsSimpleType(dummy_annotated_field, dummy_pipeline)
    result: Result = field_is_not_simple_type()
    assert isinstance(result, Skip)
    assert str == result.value


def test_annotation_pipeline_no_operators(
    dummy_title_field: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # Doing Annotated but there aren't any operators, which is an error
    dummy_title_field.operators = tuple()
    field_is_container = AnnotationPipeline(dummy_title_field, dummy_pipeline)
    result: Result = field_is_container()
    assert isinstance(result, Error)
    assert 'Annotated was used with no subsequent operators' == result.msg
