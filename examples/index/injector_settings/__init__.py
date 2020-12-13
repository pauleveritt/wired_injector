from wired_injector import Injector

from examples import example_registry
from .factories import View, View


def test():
    # The app
    registry = example_registry()

    # Per "request"
    container = registry.create_container()
    injector = Injector(container)
    view: View = injector(View)
    result = view.name
    expected = 'View - My Site'

    return expected, result
