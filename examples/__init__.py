from wired import ServiceRegistry
from wired_injector.decorators import register_injectable

from .models import view_factory, View, Customer, FrenchCustomer, Greeting, french_view_factory


def example_registry() -> ServiceRegistry:
    registry = ServiceRegistry()
    registry.register_factory(
        view_factory,
        View,
        context=Customer,
    )
    registry.register_factory(
        french_view_factory,
        View,
        context=FrenchCustomer,
    )
    register_injectable(registry, Greeting)
    return registry
