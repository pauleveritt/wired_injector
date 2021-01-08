from dataclasses import dataclass
from enum import Enum

from wired_injector import injectable
from wired_injector.operators import Get


class Phase(Enum):
    init = 10
    postinit = 20


try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore


# Site settings
@injectable()
@dataclass
class Settings:
    """ The system defines something called ``Settings`` """
    site_name: str = 'System Site'


@injectable(for_=Settings, phase=Phase.init)
@dataclass
class AppSettings:
    site_name: str = 'App Site'


# This is the one that wins due to Phase.postinit
@injectable(for_=Settings, phase=Phase.postinit)
@dataclass
class SomePluginSettings:
    site_name: str = 'Some Plugin Site'


@injectable(for_=Settings, phase=Phase.init)
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
