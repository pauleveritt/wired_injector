"""
Change order of registrations.

Usually the last registration overrides previous one. Things
are usually just scanned top to bottom. Instead, use phases to
control ordering.
"""

from wired_injector import InjectorRegistry

from .factories import View


def test():
    # The app
    registry = InjectorRegistry(use_injectables=False)
    registry.scan()

    # Per "request"
    container = registry.create_injectable_container()
    view: View = container.get(View)
    result = view.name
    expected = 'View - My Site'

    return expected, result
