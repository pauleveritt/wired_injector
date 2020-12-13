from wired_injector import InjectorRegistry

from .factories import View


def test():
    # The app
    registry = InjectorRegistry()
    registry.scan()

    # Per "request"
    container = registry.create_injectable_container()
    view = container.inject(View, view_name='Prop View')
    result = view.view_name
    expected = 'Prop View'

    return expected, result
