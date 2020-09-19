"""
Test FieldInfo from parameters on a function.
"""
from inspect import signature
from typing import Optional, List

from wired import ServiceContainer
from wired_injector.field_info import function_field_info_factory, FieldInfo


def _get_field_infos(target) -> List[FieldInfo]:
    # This is usually done by the thing that processes each field

    sig = signature(target)
    parameters = sig.parameters.values()
    field_infos = [
        function_field_info_factory(param)
        for param in parameters
    ]
    return field_infos


def test_function_one_typed_parameters():
    def target(container: ServiceContainer):
        return 99

    field_infos = _get_field_infos(target)
    assert field_infos[0].field_name == 'container'
    assert field_infos[0].field_type == ServiceContainer
    assert field_infos[0].service_type is None
    assert field_infos[0].default_value is None


def test_function_two_parameters():
    def target(container: ServiceContainer, customer_name: str):
        return 99

    field_infos = _get_field_infos(target)
    assert field_infos[0].field_name == 'container'
    assert field_infos[0].field_type == ServiceContainer
    assert field_infos[0].service_type is None
    assert field_infos[0].default_value is None
    assert field_infos[1].field_name == 'customer_name'
    assert field_infos[1].field_type == str
    assert field_infos[1].service_type is None
    assert field_infos[1].default_value is None


def test_function_optional():
    def target(container: Optional[ServiceContainer]):
        return 99

    field_infos = _get_field_infos(target)
    assert field_infos[0].field_name == 'container'
    assert field_infos[0].field_type == ServiceContainer
    assert field_infos[0].service_type is None
    assert field_infos[0].default_value is None


def test_function_default_value():
    def target(customer_name: str = 'Some Customer'):
        return customer_name

    field_infos = _get_field_infos(target)
    assert field_infos[0].field_name == 'customer_name'
    assert field_infos[0].field_type == str
    assert field_infos[0].service_type is None
    assert field_infos[0].default_value == 'Some Customer'
