from dataclasses import dataclass

from wired_injector import injectable
from wired_injector.operators import Get, Attr

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


# View
@injectable()
@dataclass
class View:
    site_name: Annotated[
        str,
        Get(BaseSettings),
        Attr('site_name'),
    ]

    @property
    def name(self):
        site_name = self.site_name
        return f'View - {site_name}'
