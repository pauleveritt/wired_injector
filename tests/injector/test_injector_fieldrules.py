from typing import Dict, Any

import pytest
from wired import ServiceContainer
from wired_injector.field_info import FieldInfo
from wired_injector.injector import (
    FieldIsInit,
    SkipField,
    FieldIsInProps,
    FoundValueField,
    FieldIsContainer,
    FieldMakePipeline,
)
from wired_injector.operators import Get

from examples.factories import View


class Target:
    pass


def test_is_init_false(regular_container):
    fi = FieldInfo('foo', str, None, False, ())
    field_is_init = FieldIsInit(fi, {}, regular_container)
    with pytest.raises(SkipField):
        field_is_init()


def test_is_init_true(regular_container):
    fi = FieldInfo('foo', str, None, True, ())
    field_is_init = FieldIsInit(fi, {}, regular_container)
    result = field_is_init()
    assert None is result


def test_is_in_props_no_props(regular_container):
    # No props
    fi = FieldInfo('foo', str, None, True, ())
    props: Dict[Any, Any] = {}
    field_is_props = FieldIsInProps(fi, props, regular_container)
    result = field_is_props()
    assert None is result


def test_is_in_props_not_in(regular_container):
    # There are props, but the field_name 'foo' isn't in it
    fi = FieldInfo('foo', str, None, True, ())
    props: Dict[Any, Any] = dict(notfoo=1)
    field_is_props = FieldIsInProps(fi, props, regular_container)
    result = field_is_props()
    assert None is result


def test_is_in_props_in_props(regular_container):
    # There are props passed in and the field_value is in it
    fi = FieldInfo('foo', str, None, True, ())
    props: Dict[Any, Any] = dict(foo=9999)
    field_is_props = FieldIsInProps(fi, props, regular_container)
    with pytest.raises(FoundValueField) as exc:
        field_is_props()
    assert exc.value.value == 9999


def test_is_in_system_props_no_system_props(regular_container):
    # No system props
    fi = FieldInfo('foo', str, None, True, ())
    props: Dict[Any, Any] = {}
    system_props: Dict[Any, Any] = {}
    field_is_props = FieldIsInProps(fi, props, regular_container, system_props)
    result = field_is_props()
    assert None is result


def test_is_in_system_props_not_in(regular_container):
    # There are system props, but the field_name 'foo' isn't in it
    fi = FieldInfo('foo', str, None, True, ())
    props: Dict[Any, Any] = {}
    system_props = dict(notfoo=1)
    field_is_props = FieldIsInProps(fi, props, regular_container, system_props)
    result = field_is_props()
    assert None is result


def test_is_in_system_props_in_props(regular_container):
    # There are system props passed in and the field_value is in it
    fi = FieldInfo('foo', str, None, True, ())
    props: Dict = {}
    system_props = dict(foo=9999)
    field_is_props = FieldIsInProps(fi, props, regular_container, system_props)
    with pytest.raises(FoundValueField) as exc:
        field_is_props()
    assert exc.value.value == 9999


def test_is_in_both_props_and_system_props(regular_container):
    # Props has higher precedence than system props
    fi = FieldInfo('foo', str, None, True, ())
    props: Dict[Any, Any] = dict(foo=1111)
    system_props = dict(foo=9999)
    field_is_props = FieldIsInProps(fi, props, regular_container, system_props)
    with pytest.raises(FoundValueField) as exc:
        field_is_props()
    assert exc.value.value == 1111


def test_is_not_container(regular_container):
    # The field is NOT asking for field_type=ServiceContainer
    fi = FieldInfo('foo', str, None, True, ())
    field_is_container = FieldIsContainer(fi, {}, regular_container)
    result = field_is_container()
    assert result is None


def test_is_container(regular_container):
    # The field is asking for field_type=ServiceContainer
    fi = FieldInfo('foo', ServiceContainer, None, True, ())
    field_is_container = FieldIsContainer(fi, {}, regular_container)
    with pytest.raises(FoundValueField) as exc:
        field_is_container()
    assert isinstance(exc.value.value, ServiceContainer)


def test_is_pipeline_no_pipeline_registered_type(regular_container):
    # We don't have a pipeline but we do have a container with the type
    # registered, such as:
    # view: View
    fi = FieldInfo('foo', View, None, True, ())
    field_make_pipeline = FieldMakePipeline(fi, {}, regular_container)
    with pytest.raises(FoundValueField) as exc:
        field_make_pipeline()
    assert exc.value.value.name == 'View'


def test_is_pipeline_get(regular_container):
    # There is a pipeline that does one thing
    pipeline = (Get(View),)
    fi = FieldInfo('foo', str, None, True, pipeline)
    field_make_pipeline = FieldMakePipeline(fi, {}, regular_container)
    with pytest.raises(FoundValueField) as exc:
        field_make_pipeline()
    assert exc.value.value.name == 'View'


def test_is_pipeline_no_pipeline_type_error(regular_container):
    # No pipeline but looking up a type that is built-in and
    # trying to look it up causes a TypeError in wired, e.g.
    # customer_name: str = 'Customer Name'
    pipeline = ()
    fi = FieldInfo('foo', str, None, True, pipeline)
    field_make_pipeline = FieldMakePipeline(fi, {}, regular_container)
    with pytest.raises(SkipField):
        field_make_pipeline()


def test_is_pipeline_no_pipeline_lookup_error(regular_container):
    # No pipeline but looking up a type that *might* be in wired such
    # as a user-defined class, but isn't registered.
    class Bar:
        pass

    pipeline = ()
    fi = FieldInfo('foo', Bar, None, True, pipeline)
    field_make_pipeline = FieldMakePipeline(fi, {}, regular_container)
    with pytest.raises(SkipField):
        field_make_pipeline()
