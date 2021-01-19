from typing import Dict, Any

import pytest
from wired import ServiceContainer
from wired_injector.pipeline2 import (
    Container,
    FieldInfo, Result, Pipeline,
)
from wired_injector.pipeline2.results import Init, Skip, Found, Error
from wired_injector.pipeline2.rules import (
    DefaultFieldInfo,
    IsInit,
    IsInProps,
    IsContainer,
    AnnotationPipeline,
)


@pytest.fixture
def dummy_field_info() -> FieldInfo:
    df = DefaultFieldInfo(
        field_name='title',
        field_type=str,
        default_value=None,
        init=False,
        operators=tuple(),
    )
    return df


def test_default_field_info(dummy_field_info: FieldInfo) -> None:
    # Ensure it meets the protocol
    meets_protocol: FieldInfo = dummy_field_info
    assert meets_protocol

    dfi = dummy_field_info
    assert dfi.field_name == 'title'


def test_is_init_false(
    dummy_field_info: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # FieldIsInit rule on a field with init=False
    dummy_field_info.init = False
    field_is_init = IsInit(dummy_field_info, dummy_pipeline)
    result: Result = field_is_init()
    assert isinstance(result, Init)
    assert str == result.value


def test_is_init_true(
    dummy_field_info: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # FieldIsInit rule on a field with init=True
    dummy_field_info.init = True
    field_is_init = IsInit(dummy_field_info, dummy_pipeline)
    result: Result = field_is_init()
    assert isinstance(result, Skip)
    assert str == result.value


def test_is_in_props_no_props(
    dummy_field_info: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # No props
    props: Dict[Any, Any] = {}
    field_is_props = IsInProps(dummy_field_info, dummy_pipeline)
    result: Result = field_is_props()
    assert isinstance(result, Skip)
    assert str == result.value


def test_is_in_props_not_in(
    dummy_field_info: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # There are props, but the field_name 'foo' isn't in it
    dummy_pipeline.props = dict(nottitle=1)
    field_is_props = IsInProps(dummy_field_info, dummy_pipeline)
    result: Result = field_is_props()
    assert isinstance(result, Skip)
    assert str == result.value


def test_is_in_props_in_props(
    dummy_field_info: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # There are props passed in and the field_value is in it
    dummy_pipeline.props = dict(title='In Props')
    field_is_props = IsInProps(dummy_field_info, dummy_pipeline)
    result: Result = field_is_props()
    assert isinstance(result, Found)
    assert 'In Props' == result.value


def test_is_in_system_props_no_system_props(
    dummy_field_info: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # No system props
    dummy_pipeline.props = {}
    dummy_pipeline.system_props = {}
    field_is_props = IsInProps(dummy_field_info, dummy_pipeline)
    result: Result = field_is_props()
    assert isinstance(result, Skip)
    assert str == result.value


def test_is_in_system_props_not_in(
    dummy_field_info: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # There are system props, but the field_name 'foo' isn't in it
    dummy_pipeline.props = {}
    dummy_pipeline.system_props = dict(notfoo=1)
    field_is_props = IsInProps(dummy_field_info, dummy_pipeline)
    result: Result = field_is_props()
    assert isinstance(result, Skip)
    assert str == result.value


def test_is_in_system_props_in_props(
    dummy_field_info: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # There are system props passed in and the field_value is in it
    dummy_pipeline.props = {}
    dummy_pipeline.system_props = dict(title='In System Props')
    field_is_props = IsInProps(dummy_field_info, dummy_pipeline)
    result: Result = field_is_props()
    assert isinstance(result, Found)
    assert 'In System Props' == result.value


def test_is_in_both_props_and_system_props(
    dummy_field_info: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # Props has higher precedence than system props
    dummy_pipeline.props = dict(title='In Props')
    dummy_pipeline.system_props = dict(title='In System Props')
    field_is_props = IsInProps(dummy_field_info, dummy_pipeline)
    result: Result = field_is_props()
    assert isinstance(result, Found)
    assert 'In Props' == result.value


def test_is_not_container(
    dummy_field_info: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # The field is NOT asking for field_type=ServiceContainer
    field_is_container = IsContainer(dummy_field_info, dummy_pipeline)
    result: Result = field_is_container()
    assert isinstance(result, Skip)
    assert str == result.value


def test_is_container(
    dummy_field_info: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    dummy_field_info.field_type = ServiceContainer
    field_is_container = IsContainer(dummy_field_info, dummy_pipeline)
    result: Result = field_is_container()
    assert isinstance(result, Found)
    assert dummy_pipeline.container == result.value


def test_annotation_pipeline_no_operators(
    dummy_field_info: FieldInfo,
    dummy_pipeline: Pipeline,
) -> None:
    # Doing Annotated but there aren't any operators, which is an error
    dummy_field_info.operators = tuple()
    field_is_container = AnnotationPipeline(dummy_field_info, dummy_pipeline)
    result: Result = field_is_container()
    assert isinstance(result, Error)
    assert 'Annotated was used with no subsequent operators' == result.msg
