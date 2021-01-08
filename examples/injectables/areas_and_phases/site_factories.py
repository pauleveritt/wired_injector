from dataclasses import dataclass

from wired_injector import injectable

from .constants import Phase
from .system_factories import Settings

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore


# Let's use phases to make this one the highest priority, by
# registering it for the "postinit" phase while the others
# are in the "init" phase.
@injectable(for_=Settings, phase=Phase.postinit)
@dataclass
class SiteSettings1:
    """ This is the one that should go last """

    site_name: str = 'My Site 1'

    @property
    def name(self):
        return f'View - {self.site_name}'


@injectable(for_=Settings, phase=Phase.init)
@dataclass
class SiteSettings2:
    """ This is the one that should go last """

    site_name: str = 'My Site 2'

    @property
    def name(self):
        return f'View - {self.site_name}'


@injectable(for_=Settings, phase=Phase.init)
@dataclass
class SiteSettings3:
    """ This is the one that should go last """

    site_name: str = 'My Site 3'

    @property
    def name(self):
        return f'View - {self.site_name}'
