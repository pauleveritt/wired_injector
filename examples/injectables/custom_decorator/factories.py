from dataclasses import dataclass

from wired_injector import injectable
from wired_injector.operators import Get

from .constants import Phase
from .decorators import config

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore # noqa: F401


# System settings
@config()
@dataclass
class Settings:
    """ The system defines something called ``Settings`` """

    site_name: str = 'System Site'


@config(for_=Settings, phase=Phase.postinit)
@dataclass
class AppSettings:
    site_name: str = 'App Site'


@config(for_=Settings)
@dataclass
class SomePluginSettings:
    site_name: str = 'Some Plugin Site'


@config(for_=Settings)
@dataclass
class SiteSettings:
    """ This is the one that should go last """

    site_name: str = 'My Site'


@injectable()
@dataclass
class View:
    site_name: Annotated[str, Get(Settings, attr='site_name')]

    @property
    def name(self):
        return f'View - {self.site_name}'
