"""
Report on applied injectables.

There are uses to keeping a list of registrations. For example, if you
have a bunch of ``@config`` decorators, you can get a listing of them,
along with a "shortname" from an info structure.
"""

from wired_injector import InjectorRegistry

from . import factories
from .constants import Area, Kind
from .factories import View


def test():
    # The app
    registry = InjectorRegistry(use_injectables=True)

    # System
    registry.scan(factories)
    registry.injectables.commit(area=Area.system)

    # All done, write the injectables to the registry
    registry.injectables.apply_injectables()

    # Get all the kind=config that have a shortname
    injectables = registry.injectables.get_info(kind=Kind.config)
    results = [
        (injectable.info['shortname'], injectable.for_)
        for injectable in injectables
        if 'shortname' in injectable.info
    ]
    result = results[0][0]
    expected = 'bob'

    return result, expected
