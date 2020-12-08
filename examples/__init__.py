from importlib import import_module
from typing import Sequence, Optional

from venusian import Scanner
from wired import ServiceRegistry, ServiceContainer
from wired_injector import Injector

from . import factories
from .factories import View, Customer, FrenchCustomer, Greeting


def example_registry(
        pkg: Optional[str] = None,
        pkgs: Sequence[str] = tuple(),

) -> ServiceRegistry:
    registry = ServiceRegistry()
    scanner = Scanner(registry=registry)
    scanner.scan(factories)

    # Now scan for custom factories
    if pkg is not None:
        scannable = import_module(pkg)
        scanner.scan(scannable)
    for scannable in pkgs:
        if isinstance(scannable, str):
            scannable = import_module(scannable)
        scanner.scan(scannable)

    return registry


def example_container(some_registry) -> ServiceContainer:
    some_container = some_registry.create_container(context=Customer())
    injector = Injector(some_container)
    some_container.register_singleton(injector, Injector)
    return some_container


def example_french_container(some_registry) -> ServiceContainer:
    some_container = some_registry.create_container(
        context=FrenchCustomer()
    )
    injector = Injector(some_container)
    some_container.register_singleton(injector, Injector)
    return some_container
