from wired_injector import InjectorRegistry

from .. import plugin, site
from examples.protocols.pluggable_system.app.protocols import Customer, View


def main(customer: Customer) -> str:
    # At startup
    registry = InjectorRegistry()
    registry.scan()
    registry.scan(plugin)
    registry.scan(site)

    # Per "request"
    container = registry.create_injectable_container(
        context=customer,
    )
    container.register_singleton(customer, Customer)
    view: View = container.get(View)
    result = view()

    return result
