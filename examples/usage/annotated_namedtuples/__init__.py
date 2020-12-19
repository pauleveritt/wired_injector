from wired_injector import InjectorRegistry

from .factories import View


def test():
    registry = InjectorRegistry()
    registry.scan()  # Look for decorators in/below current package

    # Per "request"
    container = registry.create_injectable_container()
    view = container.get(View)
    result = view['name']
    expected = 'View - Another Site'

    return expected, result
