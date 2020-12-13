from examples import example_registry
from .factories import View


def test():
    # The app
    registry = example_registry()

    # Per "request"
    container = registry.create_container()
    view: View = container.get(View)
    result = view.name
    expected = 'View - My Site'

    return expected, result
