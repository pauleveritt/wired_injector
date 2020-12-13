from wired_injector import Injector

from examples import example_registry
from .factories import View


def test():
    # The app
    registry = example_registry()

    # Per "request"
    container = registry.create_container()
    injector = Injector(container)
    container.register_singleton(injector, Injector)
    view: View = injector(View)
    result = view['name']
    expected = 'View - MY SITE'

    return expected, result
