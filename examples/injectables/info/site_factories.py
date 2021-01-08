from dataclasses import dataclass

from wired_injector import injectable

from .factories import Settings

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore


@injectable(for_=Settings)
@dataclass
class SiteSettings:
    """ This is the one that should go last """
    site_name: str = 'My Site'

    @property
    def name(self):
        return f'View - {self.site_name}'
