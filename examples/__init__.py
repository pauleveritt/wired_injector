from venusian import Scanner
from wired import ServiceRegistry

from . import factories
from .factories import View, Customer, FrenchCustomer, Greeting


def example_registry() -> ServiceRegistry:
    registry = ServiceRegistry()
    scanner = Scanner(registry=registry)
    scanner.scan(factories)
    return registry
