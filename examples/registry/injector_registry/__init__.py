from wired_injector import InjectorRegistry

from .factories import View


def test():
    # The app
    registry = InjectorRegistry()
    registry.scan()

    # Per "request"
    container = registry.create_injectable_container()
    view: View = container.get(View)
    result = view.name
    expected = 'View - My Site'

    return expected, result
