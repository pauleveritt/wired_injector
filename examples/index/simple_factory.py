"""
Simplest example of wired app.
"""
from dataclasses import dataclass

from wired import service_factory

from examples import example_registry


@service_factory()
@dataclass
class View:
    name: str = 'View'

    @classmethod
    def __wired_factory__(cls, container):
        return cls()


# The app
registry = example_registry(__package__)

# Per "request"
container = registry.create_container()
view: View = container.get(View)
result = view.name
expected = 'View'


def test():
    return expected, result
