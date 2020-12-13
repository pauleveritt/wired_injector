from wired_injector import InjectorRegistry

from .factories import View


def test():
    # The app
    registry = InjectorRegistry()
    registry.scan()

    # Per "request"
    container = registry.create_container()
    view: View = container.get(View)
    result = view.name
    expected = 'View'

    return expected, result
