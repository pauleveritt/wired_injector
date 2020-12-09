"""
The injector can sniff at function parameters.
"""
from typing import NamedTuple

from wired_injector import injectable, Injector
from wired_injector.operators import Get

from examples import example_registry

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore


class Settings:
    site_name: str


@injectable(for_=Settings)
class MySettings(NamedTuple):
    site_name: str = 'My Site'

    @property
    def upper_name(self):
        return self.site_name.upper()


# Injectable function
@injectable()
def View(
        settings: Annotated[MySettings, Get(Settings)]

):
    site_name = settings.upper_name
    return dict(name=f'View - {site_name}')


# The app
registry = example_registry(__package__)

# Per "request"
container = registry.create_container()
injector = Injector(container)
container.register_singleton(injector, Injector)
view: View = injector(View)
result = view['name']
expected = 'View - MY SITE'


def test():
    return expected, result
