from wired_injector import InjectorRegistry

from .factories import View, Customer


def test():
    registry = InjectorRegistry()
    registry.scan()  # Look for decorators in/below current package

    # Per "request"
    customer = Customer()
    container = registry.create_injectable_container(
        context=customer,
    )
    view: View = container.get(View)
    result = view.name
    expected = 'Hello Fred'

    return expected, result
