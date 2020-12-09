"""
A pipeline of operators.
"""
from dataclasses import dataclass

from wired_injector import injectable, Injector
from wired_injector.operators import Get, Attr

from examples import example_registry

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore


class Settings:
    site_name: str


@injectable(for_=Settings)
@dataclass
class MySettings:
    site_name: str = 'My Site'

    @property
    def upper_name(self):
        return self.site_name.upper()


# Injectable view
@injectable()
@dataclass
class View:
    site_name: Annotated[
        MySettings,
        Get(Settings),
        Attr('upper_name'),
    ]

    @property
    def name(self):
        return f'View - {self.site_name}'


# The app
registry = example_registry(__package__)

# Per "request"
container = registry.create_container()
injector = Injector(container)
container.register_singleton(injector, Injector)
view: View = injector(View)
result = view.name
expected = 'View - MY SITE'


def test():
    return expected, result
