from wired_injector import InjectorRegistry, Injector

from .factories import View


def test():
    # The app
    registry = InjectorRegistry()
    registry.scan()

    # Per "request"
    container = registry.create_injectable_container()
    view_class: View = container.get(View)
    injector = container.get(Injector)
    view = injector(view_class)
    result = view.name
    expected = 'Custom View'

    return expected, result
