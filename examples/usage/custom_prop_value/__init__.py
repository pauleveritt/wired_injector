from wired_injector import InjectorRegistry

from .factories import View


def test():
    registry = InjectorRegistry()
    registry.scan()  # Look for decorators in/below current package

    # Per "request"
    container = registry.create_injectable_container()
    view: View = container.inject(View, site_name='Prop Site')
    result = view.name
    expected = 'View - Prop Site'

    return expected, result
