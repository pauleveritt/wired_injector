from typing import Optional

from wired import ServiceContainer
from wired_injector.injector import Injector

from .conftest import Customer


def test_construction(this_container):
    injector = Injector(this_container)
    assert injector


def test_one_parameter_unannotated(this_container):
    def target(container: ServiceContainer):
        customer = container.get(Customer)
        return customer

    injector = Injector(this_container)
    result = injector(target)
    assert result.name == 'Some Customer'


def test_two_parameters_unannotated(this_container):
    def target(container: ServiceContainer, customer: Customer):
        return customer

    injector = Injector(this_container)
    result: Customer = injector(target)
    assert result.name == 'Some Customer'


def test_optional_unannotated(this_container):
    def target(container: Optional[ServiceContainer]):
        customer = container.get(Customer)
        return customer

    injector = Injector(this_container)
    result = injector(target)
    assert result.name == 'Some Customer'


def test_props_unannotated(this_container):
    def target(container: ServiceContainer):
        return container

    injector = Injector(this_container)
    result = injector(target, container=88)
    assert 88 == result
