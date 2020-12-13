from venusian import Scanner
from wired import ServiceRegistry

from examples.registry.regular_registry import factories
from .factories import View


def test():
    # The app
    registry = ServiceRegistry()
    scanner = Scanner(registry=registry)
    scanner.scan(factories)

    # Per "request"
    container = registry.create_container()
    view: View = container.get(View)
    result = view.name
    expected = 'View - My Site'

    return expected, result
