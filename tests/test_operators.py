import pytest
from wired import ServiceRegistry, ServiceContainer
from wired_injector.operators import Get, Attr, process_pipeline

from .conftest import Customer, FrenchCustomer


@pytest.fixture
def this_container() -> ServiceContainer:
    registry = ServiceRegistry()
    customer = Customer()
    registry.register_singleton(customer, Customer)
    french_customer = FrenchCustomer()
    registry.register_singleton(french_customer, FrenchCustomer)
    container = registry.create_container()
    return container


def test_get(this_container):
    get = Get(FrenchCustomer)
    previous = Customer
    result: FrenchCustomer = get(previous, this_container)
    assert result.name == 'French Customer'


def test_attr(this_container):
    attr = Attr('name')
    previous = FrenchCustomer()
    result = attr(previous, this_container)
    assert 'French Customer' == result


def test_get_then_attr(this_container):
    get = Get(FrenchCustomer)
    start = Customer
    result1 = get(start, this_container)
    attr = Attr('name')
    result = attr(result1, this_container)
    assert 'French Customer' == result


def test_pipeline_one(this_container):
    pipeline = (Get(FrenchCustomer),)
    result: FrenchCustomer = process_pipeline(
        this_container,
        pipeline,
        start=Customer,
    )
    assert result.name == 'French Customer'


def test_pipeline_two(this_container):
    pipeline = (Get(FrenchCustomer), Attr('name'))
    result = process_pipeline(
        this_container,
        pipeline,
        start=Customer,
    )
    assert 'French Customer' == result
