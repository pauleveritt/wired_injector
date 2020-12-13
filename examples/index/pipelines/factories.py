from dataclasses import dataclass

from wired_injector import injectable
from wired_injector.operators import Get, Attr

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
