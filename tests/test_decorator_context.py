"""
A decorator usage that customizes for a context.
"""
from dataclasses import dataclass

import pytest
from wired import ServiceRegistry
from wired.dataclasses import register_dataclass
from wired_injector import injectable, Injector
from wired_injector.operators import Attr, Context, Get

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore


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
def registry() -> ServiceRegistry:
    import sys
    from venusian import Scanner

    registry = ServiceRegistry()
    scanner = Scanner(registry=registry)
    current_module = sys.modules[__name__]
    scanner.scan(current_module)
    return registry


def test_injectable_no_context(registry):
    """ Lookup without context should get View """
    container = registry.create_container()
    injector = Injector(container)
    view_class = container.get(View)
    view: View = injector(view_class)
    assert 'View' == view.name


def test_injectable_customer_context(registry):
    """ Lookup with Customer context should get View """

    context = Customer()
    container = registry.create_container(context=context)
    injector = Injector(container)
    view_class = container.get(View)
    view: View = injector(view_class)
    assert 'View' == view.name


def test_injectable_french_context(registry):
    """ Custom context gets custom View"""

    context = FrenchCustomer()
    container = registry.create_container(context=context)
    injector = Injector(container)
    view_class = container.get(View)
    view: FrenchView = injector(view_class)
    assert 'French View' == view.name
