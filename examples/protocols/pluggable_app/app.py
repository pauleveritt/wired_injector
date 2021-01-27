from wired_injector import InjectorRegistry

from .models import AmericanCustomer, FrenchCustomer
from .protocols import Customer, View


def main(customer: Customer) -> str:
    # At startup
    registry = InjectorRegistry()
    registry.scan()  # Look for decorators in/below current package

    # Per "request"
    container = registry.create_injectable_container(
        context=customer,
    )
    container.register_singleton(customer, Customer)
    view: View = container.get(View)
    result = view()

    return result
