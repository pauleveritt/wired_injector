"""
Simplest example, just configures registry to track injectables.

No other changes.
"""
from enum import Enum

from wired_injector import InjectorRegistry

from .factories import View


class Area(Enum):
    system = 1


def test():
    # The app
    registry = InjectorRegistry(use_injectables=True)
    registry.scan()
    registry.injectables.commit(area=Area.system)
    registry.injectables.apply_injectables()

    # Per "request"
    container = registry.create_injectable_container()
    view: View = container.get(View)
    result = view.name
    expected = 'View - My Site'

    return expected, result
