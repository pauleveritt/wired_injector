import pytest
from wired import ServiceContainer, ServiceRegistry
from wired_injector.injector import Injector


@pytest.fixture
def this_container() -> ServiceContainer:
    r = ServiceRegistry()
    c = r.create_container()
    return c


def test_construction(this_container):
    injector = Injector(this_container)
    assert injector


def test_one_parameter(this_container):
    def target(container: ServiceContainer):
        return 99

    injector = Injector(this_container)
    result = injector(target)
    assert 99 == result


def test_props(this_container):
    def target(container: ServiceContainer):
        return container

    injector = Injector(this_container)
    result = injector(target, container=88)
    assert 88 == result
