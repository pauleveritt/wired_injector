from typing import NamedTuple

from wired_injector import injectable
from wired_injector.pipeline.operators import Get

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore # noqa: F401


@injectable()
class BaseSettings(NamedTuple):
    site_name: str = 'My Site'


@injectable(for_=BaseSettings)
class MySettings(NamedTuple):
    site_name: str = 'Another Site'


# Injectable function
@injectable()
def View(settings: Annotated[MySettings, Get(BaseSettings)]):
    site_name = settings.site_name
    name = f'View - {site_name}'
    return dict(name=name)
