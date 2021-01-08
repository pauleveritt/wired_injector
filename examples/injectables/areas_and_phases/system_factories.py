from dataclasses import dataclass

from wired_injector import injectable
from wired_injector.operators import Get

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore


# System settings
@injectable()
@dataclass
class Settings:
    """ The system defines something called ``Settings`` """

    site_name: str = 'System Site'


@injectable()
@dataclass
class View:
    site_name: Annotated[str, Get(Settings, attr='site_name')]

    @property
    def name(self):
        return f'View - {self.site_name}'
