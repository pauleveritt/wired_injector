"""
Injectable view which doesn't need the ``__wired_factory__`` protocol.
"""
from dataclasses import dataclass

from wired_injector import injectable, Injector

from examples import example_registry


@injectable()
@dataclass
class View:
    name: str = 'View'


# The app
registry = example_registry(__package__)

# Per "request"
container = registry.create_container()
injector = Injector(container)
view: View = injector(View)
result = view.name
expected = 'View'


def test():
    return expected, result
