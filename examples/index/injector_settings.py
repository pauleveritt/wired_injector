"""
A view with a value that depends on something else.
"""
from dataclasses import dataclass

from wired_injector import injectable, Injector

from examples import example_registry


@injectable()
@dataclass
class Settings:
    site_name: str = 'My Site'


# Injectable view
@injectable()
@dataclass
class View:
    settings: Settings

    @property
    def name(self):
        site_name = self.settings.site_name
        return f'View - {site_name}'


# The app
registry = example_registry(__package__)

# Per "request"
container = registry.create_container()
injector = Injector(container)
view: View = injector(View)
result = view.name
expected = 'View - My Site'


def test():
    return expected, result
