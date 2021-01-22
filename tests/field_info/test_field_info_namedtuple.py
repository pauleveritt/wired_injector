"""
Test FieldInfo from fields on a namedtuple class.
"""
from inspect import signature
from typing import Optional, List, NamedTuple

from wired import ServiceContainer
from wired_injector.field_info import function_field_info_factory
from wired_injector.operators import Get
from wired_injector.pipeline2 import FieldInfo

from examples.factories import Customer, FrenchCustomer

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore  # noqa: F401


def _get_field_infos(target) -> List[FieldInfo]:
    # This is usually done by the thing that processes each field

    # Exact same as for functions
    sig = signature(target)
    parameters = sig.parameters.values()
    field_infos = [function_field_info_factory(param) for param in parameters]
    return field_infos


# Damn, mypy bug with nested named tuples
# https://github.com/python/mypy/issues/7281
class Target1(NamedTuple):
    container: ServiceContainer


def test_one_typed_parameters():
    field_infos = _get_field_infos(Target1)
    assert field_infos[0].field_name == 'container'
    assert field_infos[0].field_type == ServiceContainer
    assert field_infos[0].default_value is None


class Target2(NamedTuple):
    container: ServiceContainer
    customer_name: str


def test_two_parameters():
    field_infos = _get_field_infos(Target2)
    assert field_infos[0].field_name == 'container'
    assert field_infos[0].field_type == ServiceContainer
    assert field_infos[0].default_value is None
    assert field_infos[1].field_name == 'customer_name'
    assert field_infos[1].field_type == str
    assert field_infos[1].default_value is None


class Target3(NamedTuple):
    container: Optional[ServiceContainer]


def test_optional():
    field_infos = _get_field_infos(Target3)
    assert field_infos[0].field_name == 'container'
    assert field_infos[0].field_type == ServiceContainer
    assert field_infos[0].default_value is None


class Target4(NamedTuple):
    customer_name: str = 'Some Customer'


def test_default_value():
    field_infos = _get_field_infos(Target4)
    assert field_infos[0].field_name == 'customer_name'
    assert field_infos[0].field_type == str
    assert field_infos[0].default_value == 'Some Customer'


class Target5(NamedTuple):
    container: ServiceContainer
    customer_name: str


def test_namedtuple_two_parameters():
    field_infos = _get_field_infos(Target5)
    assert field_infos[0].field_name == 'container'
    assert field_infos[0].field_type == ServiceContainer
    assert field_infos[0].default_value is None
    assert field_infos[1].field_name == 'customer_name'
    assert field_infos[1].field_type == str
    assert field_infos[1].default_value is None


class Target6(NamedTuple):
    customer: Annotated[Customer, Get(FrenchCustomer)]


def test_annotation():
    field_infos = _get_field_infos(Target6)
    assert (Get(FrenchCustomer),) == field_infos[0].operators
