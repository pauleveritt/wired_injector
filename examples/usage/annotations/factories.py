from dataclasses import dataclass

from wired_injector import injectable
from wired_injector.pipeline.operators import Get

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore # noqa: F401


@injectable()
@dataclass
class BaseSettings:
    site_name: str = 'My Site'


@injectable(for_=BaseSettings)
@dataclass
class MySettings:
    site_name: str = 'Another Site'


@injectable()
@dataclass
class View:
    settings: Annotated[MySettings, Get(BaseSettings)]

    @property
    def name(self):
        site_name = self.settings.site_name
        return f'View - {site_name}'
