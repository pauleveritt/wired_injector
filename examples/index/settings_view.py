"""
A view with a value that depends on something else.
"""
from dataclasses import dataclass

from wired import service_factory
from wired_injector import injectable

from examples import example_registry


# Site settings
@injectable()
@dataclass
class Settings:
    site_name: str = 'My Site'


@service_factory()
@dataclass
class View:
    name: str = 'View'

    @classmethod
    def __wired_factory__(cls, container):
        settings: Settings = container.get(Settings)
        site_name = settings.site_name
        name = f'View - {site_name}'
        return cls(name=name)


# The app
registry = example_registry(__package__)

# Per "request"
container = registry.create_container()
view: View = container.get(View)
result = view.name
expected = 'View - My Site'


def test():
    return expected, result
