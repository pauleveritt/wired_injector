from wired import ServiceRegistry

from .factories import View


def test():
    registry = ServiceRegistry()
    registry.register_factory(View, View)

    # Per "request"
    container = registry.create_container()
    view: View = container.get(View)
    result = view.name
    expected = 'View'

    return expected, result
