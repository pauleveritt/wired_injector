"""
Simplest example, just configures registry to track injectables.

No other changes.
"""

from wired_injector import InjectorRegistry

from .factories import View


def test():
    # The app
    registry = InjectorRegistry(use_injectables=True)
    registry.scan()

    # Per "request"
    container = registry.create_injectable_container()
    view: View = container.get(View)
    result = view.name
    expected = 'View - My Site'

    return expected, result
