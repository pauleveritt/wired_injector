"""
Report on applied injectables.

There are uses to keeping a list of registrations. For example, if you
have a bunch of ``@config`` decorators, you can get a listing of them,
along with a "shortname" from an info structure.
"""

from wired_injector import InjectorRegistry

from . import factories
from .contants import Area
from .factories import View


def test():
    # The app
    registry = InjectorRegistry(use_injectables=True)

    # System
    registry.scan(factories)
    registry.injectables.commit(area=Area.system)

    # All done, write the injectables to the registry
    registry.injectables.apply_injectables()

    # Per "request"
    container = registry.create_injectable_container()
    view: View = container.get(View)
    result = view.name
    expected = 'View - System Site'

    return result, expected
