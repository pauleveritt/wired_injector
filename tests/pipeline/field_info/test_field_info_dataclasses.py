"""
Test FieldInfo from fields on a dataclass.
"""
from dataclasses import dataclass, field
import typing
from typing import Optional, Tuple

from wired_injector.pipeline.operators import Get

from ..conftest import _get_field_infos


class Customer:
    pass


class FrenchCustomer(Customer):
    pass


try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore  # noqa: F401


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


def test_more_generic():
    @dataclass
    class View:
        customer_name: Tuple[str, ...]

    field_infos = _get_field_infos(View)
    assert field_infos[0].field_name == 'customer_name'
    ga = getattr(typing, '_GenericAlias')
    assert isinstance(field_infos[0].field_type, ga)
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
    assert field_infos[0].has_annotated is False


def test_annotation():
    @dataclass
    class View:
        customer_name: Annotated[Customer, Get(FrenchCustomer)]

    field_infos = _get_field_infos(View)
    assert field_infos[0].field_name == 'customer_name'
    assert field_infos[0].field_type is Customer
    assert field_infos[0].default_value is None
    assert field_infos[0].operators == (Get(FrenchCustomer),)
    assert field_infos[0].has_annotated is True


def test_optional():
    @dataclass
    class View:
        customer_name: Optional[Annotated[Customer, Get(FrenchCustomer)]]

    field_infos = _get_field_infos(View)
    assert field_infos[0].field_name == 'customer_name'
    assert field_infos[0].field_type is Customer
    assert field_infos[0].default_value is None
    assert field_infos[0].operators == (Get(FrenchCustomer),)
