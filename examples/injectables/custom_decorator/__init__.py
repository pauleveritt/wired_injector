"""
Custom decorator that sets a default "phase".

Here we make a ``@config`` directive as an alias for
``@injectable(phase=Phase.init)``. Thus, instead of
``phase=None``, all their injectables get
``phase=Phase.init``.

To kind of see it in action, we change the injectable for
``.factories.AppSettings`` to "win" by passing in a
higher-priority.
"""

from wired_injector import InjectorRegistry

from .constants import Area
from .factories import View


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
    expected = 'View - App Site'

    return result, expected
