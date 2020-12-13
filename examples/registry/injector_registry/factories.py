from dataclasses import dataclass

from wired import service_factory
from wired_injector import injectable


# Site settings
@injectable()
@dataclass
class Settings:
    site_name: str = 'My Site'


@service_factory()
@dataclass
class View:
    name: str = 'iew'

    @classmethod
    def __wired_factory__(cls, container):
        settings: Settings = container.get(Settings)
        site_name = settings.site_name
        name = f'View - {site_name}'
        return cls(name=name)

