from wired_injector import Injector, InjectorRegistry

from .factories import View


def test():
    # The app
    registry = InjectorRegistry()
    registry.scan()

    # Per "request"
    container = registry.create_injectable_container()
    injector = container.get(Injector)
    view: View = injector(View)
    result = view.name
    expected = 'View - MY SITE'

    return expected, result
