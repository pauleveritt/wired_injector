from dataclasses import dataclass
from typing import Protocol

import pytest
from wired import ServiceContainer, ServiceRegistry
from wired_injector import Injector
from wired_injector.decorators import register_injectable
from wired_injector.operators import Get

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


class RegularCustomer:
    name: str

    def __init__(self):
        self.name = 'Some Customer'


class FrenchCustomer:
    name: str

    def __init__(self):
        self.name = 'French Customer'


class View(Protocol):
    name: str


class RegularView(View):
    name: str

    def __init__(self):
        self.name = 'Regular View'

    def __call__(self):
        return self.name

    @property
    def caps_name(self):
        return self.name.upper()


class FrenchView(View):
    name: str

    def __init__(self):
        self.name = 'French View'

    def __call__(self):
        return self.name

    @property
    def caps_name(self):
        return self.name.upper()


@dataclass
class Greeting:
    customer_name: Annotated[
        str,
        Get(View, attr='caps_name')
    ]

    def __call__(self):
        return f'Hello {self.customer_name}'


def regular_view_factory(container):
    return RegularView()


def french_view_factory(container):
    return FrenchView()


@pytest.fixture
def this_registry() -> ServiceRegistry:
    registry = ServiceRegistry()
    registry.register_factory(regular_view_factory, View, context=RegularCustomer)
    registry.register_factory(french_view_factory, View, context=FrenchCustomer)
    register_injectable(registry, Greeting)
    return registry


@pytest.fixture
def regular_container(this_registry) -> ServiceContainer:
    c = this_registry.create_container(context=RegularCustomer())
    injector = Injector(c)
    c.register_singleton(injector, Injector)
    return c


@pytest.fixture
def french_container(this_registry) -> ServiceContainer:
    c = this_registry.create_container(context=FrenchCustomer())
    injector = Injector(c)
    c.register_singleton(injector, Injector)
    return c


@pytest.fixture
def regular_injector(regular_container):
    i: Injector = regular_container.get(Injector)
    return i


@pytest.fixture
def french_injector(french_container):
    i: Injector = french_container.get(Injector)
    return i
