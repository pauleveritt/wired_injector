"""
A decorator usage that overrides another registration.
"""
from dataclasses import dataclass

import pytest
from wired import ServiceRegistry
from wired_injector import injectable, Injector

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore


@dataclass
class View:
    name: str = 'View'


class view(injectable):
    for_ = View


@view()
@dataclass
class OverriddenView:
    name: str = 'Overridden View'


@pytest.fixture
def registry() -> ServiceRegistry:
    import sys
    from venusian import Scanner

    registry = ServiceRegistry()
    scanner = Scanner(registry=registry)
    current_module = sys.modules[__name__]
    scanner.scan(current_module)
    return registry


def test_injectable_overridden(registry):
    container = registry.create_container()
    injector = Injector(container)
    view_class = container.get(View)
    v: OverriddenView = injector(view_class)
    assert 'Overridden View' == v.name
