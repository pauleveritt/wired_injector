from dataclasses import dataclass

from wired_injector import injectable


@injectable()
@dataclass
class BaseSettings:
    site_name: str = 'My Site'


@injectable(for_=BaseSettings)
@dataclass
class MySettings:
    site_name: str = 'Another Site'


@injectable()
@dataclass
class View:
    settings: BaseSettings

    @property
    def name(self):
        site_name = self.settings.site_name
        return f'View - {site_name}'
