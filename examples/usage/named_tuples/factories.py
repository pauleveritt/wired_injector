from typing import NamedTuple

from wired_injector import injectable


# Site settings
@injectable()
class Settings(NamedTuple):
    site_name: str = 'My Site'


# View that uses site settings
@injectable()
class View(NamedTuple):
    settings: Settings

    @property
    def name(self):
        site_name = self.settings.site_name
        return f'View - {site_name}'
