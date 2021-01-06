"""
Areas and phases combined.

Mimic an actual system with areas and phases.
"""

from wired_injector import InjectorRegistry

from . import (
    system_factories,
    app_factories,
    plugin_factories,
    site_factories,
)
from .constants import Area
from .system_factories import View


def test():
    # The app
    registry = InjectorRegistry(use_injectables=True)

    # System
    registry.scan(system_factories)
    registry.injectables.commit(area=Area.system)

    # App
    registry.scan(app_factories)
    registry.injectables.commit(area=Area.app)

    # Plugins
    registry.scan(plugin_factories)
    registry.injectables.commit(area=Area.plugins)

    # Site
    registry.scan(site_factories)
    registry.injectables.commit(area=Area.site)

    # All done, write the injectables to the registry
    registry.injectables.apply_injectables()

    # Per "request"
    container = registry.create_injectable_container()
    view: View = container.get(View)
    result = view.name
    expected = 'View - My Site 1'

    return result, expected
