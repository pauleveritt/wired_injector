"""
A decorator usage that customizes for a context.
"""
from dataclasses import dataclass

import pytest
from wired_injector import injectable, InjectorRegistry

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore  # noqa: F401


@dataclass
class Customer:
    name: str = 'Customer'


@dataclass
class FrenchCustomer:
    name: str = 'French Customer'


@injectable()
@dataclass
class View:
    name: str = 'View'


@injectable(for_=View, context=FrenchCustomer)
@dataclass
class FrenchView:
    name: str = 'French View'


@pytest.fixture
def registry() -> InjectorRegistry:
    registry = InjectorRegistry()
    registry.scan()
    return registry


def test_injectable_no_context(registry):
    """ Lookup without context should get View """
    container = registry.create_injectable_container()
    view: View = container.get(View)
    assert 'View' == view.name


def test_injectable_customer_context(registry):
    """ Lookup with Customer context should get View """

    context = Customer()
    container = registry.create_injectable_container(context=context)
    view: View = container.get(View)
    assert 'View' == view.name


def test_injectable_french_context(registry):
    """ Custom context gets custom View"""

    context = FrenchCustomer()
    container = registry.create_injectable_container(context=context)
    view: View = container.get(View)
    assert 'French View' == view.name
