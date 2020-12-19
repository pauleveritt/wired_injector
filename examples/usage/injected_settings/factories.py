from dataclasses import dataclass

from wired_injector import injectable


# Site settings
@injectable()
@dataclass
class Settings:
    site_name: str = 'My Site'


# View that uses site settings
@injectable()
@dataclass
class View:
    settings: Settings

    @property
    def name(self):
        site_name = self.settings.site_name
        return f'View - {site_name}'
