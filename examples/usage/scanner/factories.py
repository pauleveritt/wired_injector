from dataclasses import dataclass

from wired import ServiceContainer, service_factory


@service_factory()
@dataclass
class View:
    name: str = 'View'

    @classmethod
    def __wired_factory__(cls, container: ServiceContainer):
        return cls()
