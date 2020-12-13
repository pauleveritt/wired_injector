from dataclasses import dataclass

from wired_injector import injectable


@injectable()
@dataclass
class Settings:
    site_name: str = 'My Site'


# Injectable view
@injectable()
@dataclass
class View:
    settings: Settings

    @property
    def name(self):
        site_name = self.settings.site_name
        return f'View - {site_name}'
