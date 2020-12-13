from wired_injector import Injector, InjectorRegistry

from .factories import View


def test():
    # The app
    registry = InjectorRegistry()
    registry.scan()

    # Per "request"
    container = registry.create_container()
    injector = Injector(container)
    view: View = injector(View)
    result = view.name
    expected = 'View'

    return expected, result
