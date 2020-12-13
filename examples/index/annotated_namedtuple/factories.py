from typing import NamedTuple

from wired_injector import injectable
from wired_injector.operators import Get

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


# Injectable NamedTuple
@injectable()
class View(NamedTuple):
    settings: Annotated[MySettings, Get(Settings)]

    @property
    def name(self):
        site_name = self.settings.upper_name
        return f'View - {site_name}'
