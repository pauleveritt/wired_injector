"""
Group registrations into "areas".

It is usually important to process the "system" registrations (such as
Themester) before an app, before plugins, and before the site
customizations.

Rather than make each use of a decoration say which area it is in, the
boundaries are laid out at setup time by grouping the batches.
"""
from enum import Enum

from wired_injector import InjectorRegistry

from . import (
    system_factories,
    app_factories,
    plugin_factories,
    site_factories,
)
from .system_factories import View


class Area(Enum):
    system = 1
    app = 2
    plugins = 3
    site = 4


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
    expected = 'View - My Site'

    return result, expected
