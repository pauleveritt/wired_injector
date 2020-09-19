from dataclasses import dataclass, field, fields
from inspect import signature
from typing import get_type_hints, Optional, List

from wired import ServiceContainer
from wired_injector.field_info import function_field_info_factory, FieldInfo, dataclass_field_info_factory


class DummyCustomer:
    pass


def _get_function_field_infos(target) -> List[FieldInfo]:
    # This is usually done by the thing that processes each field

    sig = signature(target)
    parameters = sig.parameters.values()
    field_infos = [
        function_field_info_factory(param)
        for param in parameters
    ]
    return field_infos


def _get_dataclass_field_infos(target) -> List[FieldInfo]:
    # We iterate through type hints to preserve ordering, though
    # perhaps it doesn't matter.
    type_hints = get_type_hints(target, include_extras=True)
    fields_mapping = {f.name: f for f in fields(target)}
    field_infos = [
        dataclass_field_info_factory(fields_mapping[field_name])
        for field_name in type_hints
    ]
    return field_infos


def test_function_one_typed_parameters():
    def target(container: ServiceContainer):
        return 99

    field_infos = _get_function_field_infos(target)
    assert field_infos[0].field_name == 'container'
    assert field_infos[0].field_type == ServiceContainer
    assert field_infos[0].service_type is None
    assert field_infos[0].default_value is None


def test_function_two_parameters():
    def target(container: ServiceContainer, customer_name: str):
        return 99

    field_infos = _get_function_field_infos(target)
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

    field_infos = _get_function_field_infos(target)
    assert field_infos[0].field_name == 'container'
    assert field_infos[0].field_type == ServiceContainer
    assert field_infos[0].service_type is None
    assert field_infos[0].default_value is None


def test_function_default_value():
    def target(customer_name: str = 'Some Customer'):
        return customer_name

    field_infos = _get_function_field_infos(target)
    assert field_infos[0].field_name == 'customer_name'
    assert field_infos[0].field_type == str
    assert field_infos[0].service_type is None
    assert field_infos[0].default_value == 'Some Customer'


def test_dataclass():
    @dataclass
    class View:
        customer_name: str

    field_infos = _get_dataclass_field_infos(View)
    assert field_infos[0].field_name == 'customer_name'
    assert field_infos[0].field_type == str
    assert field_infos[0].service_type is None
    assert field_infos[0].default_value is None
    assert field_infos[0].init == True


def test_dataclass_generic():
    @dataclass
    class View:
        customer_name: Optional[str]

    field_infos = _get_dataclass_field_infos(View)
    assert field_infos[0].field_name == 'customer_name'
    assert field_infos[0].field_type == str
    assert field_infos[0].service_type is None
    assert field_infos[0].default_value is None
    assert field_infos[0].init == True


def test_dataclass_init_false():
    @dataclass
    class View:
        customer_name: str = field(init=False)

    field_infos = _get_dataclass_field_infos(View)
    assert field_infos[0].field_name == 'customer_name'
    assert field_infos[0].field_type == str
    assert field_infos[0].service_type is None
    assert field_infos[0].default_value is None
    assert field_infos[0].init == False
