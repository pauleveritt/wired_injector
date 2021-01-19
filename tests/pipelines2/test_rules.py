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
    dummy_container: Container,
    dummy_pipeline: Pipeline,
    dummy_field_info: FieldInfo,
) -> None:
    # FieldIsInit rule on a field with init=False
    dummy_field_info.init = False
    field_is_init = IsInit(
        dummy_field_info, {}, dummy_container, dummy_pipeline,
    )
    result: Result = field_is_init()
    assert isinstance(result, Init)
    assert str == result.value


def test_is_init_true(
    dummy_container: Container,
    dummy_pipeline: Pipeline,
    dummy_field_info: FieldInfo,
) -> None:
    # FieldIsInit rule on a field with init=True
    dummy_field_info.init = True
    field_is_init = IsInit(
        dummy_field_info, {}, dummy_container, dummy_pipeline,
    )
    result: Result = field_is_init()
    assert isinstance(result, Skip)
    assert str == result.value


def test_is_in_props_no_props(
    dummy_container: Container,
    dummy_pipeline: Pipeline,
    dummy_field_info: FieldInfo,
) -> None:
    # No props
    props: Dict[Any, Any] = {}
    field_is_props = IsInProps(
        dummy_field_info, props, dummy_container, dummy_pipeline,
    )
    result: Result = field_is_props()
    assert isinstance(result, Skip)
    assert str == result.value


def test_is_in_props_not_in(
    dummy_container: Container,
    dummy_pipeline: Pipeline,
    dummy_field_info: FieldInfo,
) -> None:
    # There are props, but the field_name 'foo' isn't in it
    props: Dict[Any, Any] = dict(nottitle=1)
    field_is_props = IsInProps(
        dummy_field_info, props, dummy_container, dummy_pipeline,
    )
    result: Result = field_is_props()
    assert isinstance(result, Skip)
    assert str == result.value


def test_is_in_props_in_props(
    dummy_container: Container,
    dummy_pipeline: Pipeline,
    dummy_field_info: FieldInfo,
) -> None:
    # There are props passed in and the field_value is in it
    props: Dict[Any, Any] = dict(title='In Props')
    field_is_props = IsInProps(
        dummy_field_info, props, dummy_container, dummy_pipeline,
    )
    result: Result = field_is_props()
    assert isinstance(result, Found)
    assert 'In Props' == result.value


def test_is_in_system_props_no_system_props(
    dummy_container: Container,
    dummy_pipeline: Pipeline,
    dummy_field_info: FieldInfo,
) -> None:
    # No system props
    props: Dict[Any, Any] = {}
    system_props: Dict[Any, Any] = {}
    field_is_props = IsInProps(
        dummy_field_info, props, dummy_container, dummy_pipeline, system_props,
    )
    result: Result = field_is_props()
    assert isinstance(result, Skip)
    assert str == result.value


def test_is_in_system_props_not_in(
    dummy_container: Container,
    dummy_pipeline: Pipeline,
    dummy_field_info: FieldInfo,
) -> None:
    # There are system props, but the field_name 'foo' isn't in it
    props: Dict[Any, Any] = {}
    system_props = dict(notfoo=1)
    field_is_props = IsInProps(
        dummy_field_info, props, dummy_container, dummy_pipeline, system_props,
    )
    result: Result = field_is_props()
    assert isinstance(result, Skip)
    assert str == result.value


def test_is_in_system_props_in_props(
    dummy_container: Container,
    dummy_pipeline: Pipeline,
    dummy_field_info: FieldInfo,
) -> None:
    # There are system props passed in and the field_value is in it
    props: Dict[Any, Any] = {}
    system_props = dict(title='In System Props')
    field_is_props = IsInProps(
        dummy_field_info, props, dummy_container, dummy_pipeline, system_props,
    )
    result: Result = field_is_props()
    assert isinstance(result, Found)
    assert 'In System Props' == result.value


def test_is_in_both_props_and_system_props(
    dummy_container: Container,
    dummy_pipeline: Pipeline,
    dummy_field_info: FieldInfo,
) -> None:
    # Props has higher precedence than system props
    props: Dict[Any, Any] = dict(title='In Props')
    system_props = dict(title='In System Props')
    field_is_props = IsInProps(
        dummy_field_info, props, dummy_container, dummy_pipeline, system_props,
    )
    result: Result = field_is_props()
    assert isinstance(result, Found)
    assert 'In Props' == result.value


def test_is_not_container(
    dummy_container: Container,
    dummy_pipeline: Pipeline,
    dummy_field_info: FieldInfo,
) -> None:
    # The field is NOT asking for field_type=ServiceContainer
    field_is_container = IsContainer(
        dummy_field_info, {}, dummy_container, dummy_pipeline,
    )
    result: Result = field_is_container()
    assert isinstance(result, Skip)
    assert str == result.value


def test_is_container(
    dummy_container: Container,
    dummy_pipeline: Pipeline,
    dummy_field_info: FieldInfo,
) -> None:
    dummy_field_info.field_type = ServiceContainer
    field_is_container = IsContainer(
        dummy_field_info, {}, dummy_container, dummy_pipeline,
    )
    result: Result = field_is_container()
    assert isinstance(result, Found)
    assert dummy_container == result.value


def test_annotation_pipeline_no_operators(
    dummy_container: Container,
    dummy_pipeline: Pipeline,
    dummy_field_info: FieldInfo,
) -> None:
    # Doing Annotated but there aren't any operators, which is an error
    dummy_field_info.operators = tuple()
    field_is_container = AnnotationPipeline(
        dummy_field_info, {}, dummy_container, dummy_pipeline,
    )
    result: Result = field_is_container()
    assert isinstance(result, Error)
    assert 'Annotated was used with no subsequent operators' == result.msg
