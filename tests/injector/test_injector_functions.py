from typing import Optional, Annotated

from wired import ServiceContainer
from wired_injector.injector import Injector
from wired_injector.operators import Get

from ..conftest import Customer, FrenchCustomer


def test_construction(this_container):
    injector = Injector(this_container)
    assert injector


def test_one_parameter_container(this_container):
    def target(container: ServiceContainer):
        customer = container.get(Customer)
        return customer

    injector = Injector(this_container)
    result = injector(target)
    assert result.name == 'Some Customer'


def test_one_parameter_field_type(this_container):
    def target(customer: Customer):
        return customer

    injector = Injector(this_container)
    result = injector(target)
    assert result.name == 'Some Customer'


def test_one_parameter_annotated(this_container):
    this_container.register_singleton(FrenchCustomer(), Customer)

    def target(french_customer: Annotated[FrenchCustomer, Get(Customer)]):
        return french_customer

    injector = Injector(this_container)
    result = injector(target)
    assert result.name == 'French Customer'


def test_two_parameters_unannotated(this_container):
    def target(container: ServiceContainer, customer: Customer):
        return customer

    injector = Injector(this_container)
    result: Customer = injector(target)
    assert result.name == 'Some Customer'


def test_two_parameters_annotated(this_container):
    this_container.register_singleton(FrenchCustomer(), Customer)

    def target(
            container: ServiceContainer,
            french_customer: Annotated[FrenchCustomer, Get(Customer)],
    ):
        return french_customer

    injector = Injector(this_container)
    result: Customer = injector(target)
    assert result.name == 'French Customer'


def test_optional_unannotated(this_container):
    def target(container: Optional[ServiceContainer]):
        customer = container.get(Customer)
        return customer

    injector = Injector(this_container)
    result = injector(target)
    assert result.name == 'Some Customer'


def test_optional_annotated(this_container):
    this_container.register_singleton(FrenchCustomer(), Customer)

    def target(
            french_customer: Optional[Annotated[FrenchCustomer, Get(Customer)]],
    ):
        return french_customer

    injector = Injector(this_container)
    result = injector(target)
    assert result.name == 'French Customer'


def test_props_unannotated(this_container):
    def target(container: ServiceContainer):
        return container

    injector = Injector(this_container)
    result = injector(target, container=88)
    assert 88 == result
