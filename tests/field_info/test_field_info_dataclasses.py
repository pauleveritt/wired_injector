"""
Test FieldInfo from fields on a dataclass.
"""
from dataclasses import dataclass, field, fields
from typing import Optional, List

from wired_injector.field_info import FieldInfo, dataclass_field_info_factory
from wired_injector.operators import Get


class Customer:
    pass


class FrenchCustomer(Customer):
    pass


try:
    from typing import Annotated
    from typing import get_type_hints
except ImportError:
    # Need the updated get_type_hints which allows include_extras=True
    from typing_extensions import Annotated, get_type_hints


def _get_field_infos(target) -> List[FieldInfo]:
    # We iterate through type hints to preserve ordering, though
    # perhaps it doesn't matter.
    type_hints = get_type_hints(target, include_extras=True)
    fields_mapping = {f.name: f for f in fields(target)}
    field_infos = [
        dataclass_field_info_factory(fields_mapping[field_name])
        for field_name in type_hints
    ]
    return field_infos


def test():
    @dataclass
    class View:
        customer_name: str

    field_infos = _get_field_infos(View)
    assert field_infos[0].field_name == 'customer_name'
    assert field_infos[0].field_type == str
    assert field_infos[0].default_value is None
    assert field_infos[0].init is True


def test_generic():
    @dataclass
    class View:
        customer_name: Optional[str]

    field_infos = _get_field_infos(View)
    assert field_infos[0].field_name == 'customer_name'
    assert field_infos[0].field_type == str
    assert field_infos[0].default_value is None
    assert field_infos[0].init is True


def test_init_false():
    @dataclass
    class View:
        customer_name: str = field(init=False)

    field_infos = _get_field_infos(View)
    assert field_infos[0].field_name == 'customer_name'
    assert field_infos[0].field_type == str
    assert field_infos[0].default_value is None
    assert field_infos[0].init is False


def test_annotation():
    @dataclass
    class View:
        customer_name: Annotated[Customer, Get(FrenchCustomer)]

    field_infos = _get_field_infos(View)
    assert field_infos[0].field_name == 'customer_name'
    assert field_infos[0].field_type is Customer
    assert field_infos[0].default_value is None
    assert field_infos[0].pipeline == (Get(FrenchCustomer),)


def test_optional():
    @dataclass
    class View:
        customer_name: Optional[Annotated[Customer, Get(FrenchCustomer)]]

    field_infos = _get_field_infos(View)
    assert field_infos[0].field_name == 'customer_name'
    assert field_infos[0].field_type is Customer
    assert field_infos[0].default_value is None
    assert field_infos[0].pipeline == (Get(FrenchCustomer),)
