"""
A decorator usage that overrides another registration.
"""
from dataclasses import dataclass

import pytest
from wired_injector import injectable, InjectorRegistry

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore


@dataclass
class View:
    name: str = 'View'


@injectable(for_=View)
@dataclass
class OverriddenView:
    name: str = 'Overridden View'


@pytest.fixture
def registry() -> InjectorRegistry:
    registry = InjectorRegistry()
    registry.scan()
    return registry


def test_injectable_overridden(registry):
    container = registry.create_injectable_container()
    view: OverriddenView = container.get(View)
    assert 'Overridden View' == view.name
