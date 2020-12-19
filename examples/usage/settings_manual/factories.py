from dataclasses import dataclass

from wired import service_factory
from wired_injector import injectable


# Site settings
@injectable()
@dataclass
class Settings:
    site_name: str = 'My Site'


# View that uses site settings
@service_factory()
@dataclass
class View:
    name: str

    @classmethod
    def __wired_factory__(cls, container):
        settings: Settings = container.get(Settings)
        site_name = settings.site_name
        name = f'View - {site_name}'
        return cls(name=name)
