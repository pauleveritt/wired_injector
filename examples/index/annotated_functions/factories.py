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


# Injectable function
@injectable()
def View(settings: Annotated[MySettings, Get(Settings)]):
    site_name = settings.upper_name
    return dict(name=f'View - {site_name}')
