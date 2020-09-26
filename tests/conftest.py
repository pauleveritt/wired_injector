import pytest
from wired import ServiceContainer, ServiceRegistry


class RegularCustomer:
    name: str

    def __init__(self):
        self.name = 'Some Customer'


class FrenchCustomer:
    name: str

    def __init__(self):
        self.name = 'French Customer'


class View:
    pass


class RegularView:
    name: str

    def __init__(self):
        self.name = 'Regular View'


class FrenchView:
    name: str

    def __init__(self):
        self.name = 'French View'


def regular_view_factory(container):
    return RegularView()


def french_view_factory(container):
    return FrenchView()


@pytest.fixture
def this_registry() -> ServiceRegistry:
    registry = ServiceRegistry()
    registry.register_factory(regular_view_factory, View, context=RegularCustomer)
    registry.register_factory(french_view_factory, View, context=FrenchCustomer)
    return registry


@pytest.fixture
def regular_container(this_registry) -> ServiceContainer:
    c = this_registry.create_container(context=RegularCustomer())
    return c


@pytest.fixture
def french_container(this_registry) -> ServiceContainer:
    c = this_registry.create_container(context=FrenchCustomer())
    return c
