from wired import ServiceContainer
from wired_injector import Injector

from examples.factories import Customer, FrenchCustomer


def example_container(some_registry) -> ServiceContainer:
    some_container = some_registry.create_container(context=Customer())
    injector = Injector(some_container)
    some_container.register_singleton(injector, Injector)
    return some_container


def example_french_container(some_registry) -> ServiceContainer:
    some_container = some_registry.create_container(context=FrenchCustomer())
    injector = Injector(some_container)
    some_container.register_singleton(injector, Injector)
    return some_container
