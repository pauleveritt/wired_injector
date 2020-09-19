import pytest
from wired import ServiceRegistry, ServiceContainer
from wired_injector.operators import Get, Attr, process_pipeline


class Customer:
    name = 'Customer'


class FrenchCustomer(Customer):
    name = 'French Customer'


@pytest.fixture
def this_container() -> ServiceContainer:
    registry = ServiceRegistry()
    registry.register_service(Customer)
    registry.register_service(FrenchCustomer)
    container = registry.create_container()
    return container


def test_get(this_container):
    get = Get(FrenchCustomer)
    previous = Customer
    result = get(previous, this_container)
    assert FrenchCustomer is result


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
    result = process_pipeline(
        this_container,
        pipeline,
        start=Customer,
    )
    assert FrenchCustomer is result


def test_pipeline_two(this_container):
    pipeline = (Get(FrenchCustomer), Attr('name'))
    result = process_pipeline(
        this_container,
        pipeline,
        start=Customer,
    )
    assert 'French Customer' == result
