"""
Test FieldInfo from fields on a namedtuple class.
"""
from inspect import signature
from typing import Optional, List, NamedTuple

from wired import ServiceContainer
from wired_injector.field_info import function_field_info_factory, FieldInfo
from wired_injector.operators import Get

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


class Customer:
    pass


class FrenchCustomer(Customer):
    pass


def _get_field_infos(target) -> List[FieldInfo]:
    # This is usually done by the thing that processes each field

    # Exact same as for functions
    sig = signature(target)
    parameters = sig.parameters.values()
    field_infos = [
        function_field_info_factory(param)
        for param in parameters
    ]
    return field_infos


def test_one_typed_parameters():
    class Target(NamedTuple):
        container: ServiceContainer

    field_infos = _get_field_infos(Target)
    assert field_infos[0].field_name == 'container'
    assert field_infos[0].field_type == ServiceContainer
    assert field_infos[0].default_value is None


def test_two_parameters():
    class Target(NamedTuple):
        container: ServiceContainer
        customer_name: str

    field_infos = _get_field_infos(Target)
    assert field_infos[0].field_name == 'container'
    assert field_infos[0].field_type == ServiceContainer
    assert field_infos[0].default_value is None
    assert field_infos[1].field_name == 'customer_name'
    assert field_infos[1].field_type == str
    assert field_infos[1].default_value is None


def test_optional():
    class Target(NamedTuple):
        container: Optional[ServiceContainer]

    field_infos = _get_field_infos(Target)
    assert field_infos[0].field_name == 'container'
    assert field_infos[0].field_type == ServiceContainer
    assert field_infos[0].default_value is None


def test_default_value():
    class Target(NamedTuple):
        customer_name: str = 'Some Customer'

    field_infos = _get_field_infos(Target)
    assert field_infos[0].field_name == 'customer_name'
    assert field_infos[0].field_type == str
    assert field_infos[0].default_value == 'Some Customer'


def test_namedtuple_two_parameters():
    class Target(NamedTuple):
        container: ServiceContainer
        customer_name: str

    field_infos = _get_field_infos(Target)
    assert field_infos[0].field_name == 'container'
    assert field_infos[0].field_type == ServiceContainer
    assert field_infos[0].default_value is None
    assert field_infos[1].field_name == 'customer_name'
    assert field_infos[1].field_type == str
    assert field_infos[1].default_value is None


def test_annotation():
    class Target(NamedTuple):
        customer: Annotated[Customer, Get(FrenchCustomer)]

    field_infos = _get_field_infos(Target)
    assert field_infos[0].pipeline == (Get(FrenchCustomer),)
