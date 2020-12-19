from dataclasses import dataclass

from wired import ServiceContainer


@dataclass
class View:
    name: str = 'View'


def view_factory(container: ServiceContainer):
    return View()
