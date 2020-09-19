from dataclasses import dataclass
from typing import Annotated, TypeVar

import pytest
from wired import ServiceRegistry, ServiceContainer
from wired_injector import Injector, _target_type, TargetType, _inject_marker, Attr, Injected


class Customer:
    name: str = 'Base Customer'


class FrenchCustomer:
    name: str = 'French Customer'


@pytest.fixture
def this_container() -> ServiceContainer:
    r = ServiceRegistry()
    r.register_service(Customer)
    c = r.create_container()
    return c


@pytest.fixture
def french_container() -> ServiceContainer:
    r = ServiceRegistry()
    r.register_service(FrenchCustomer, for_=Customer)
    c = r.create_container(context=FrenchCustomer())
    return c


@pytest.fixture
def this_injector(this_container) -> Injector:
    return Injector(container=this_container)


@pytest.fixture
def this_injector2(french_container) -> Injector:
    return Injector(container=french_container)


class DummyService:
    """ Some marker """
    pass


def test_target_type():
    @dataclass
    class Target:
        pass

    def target():
        return

    assert TargetType.function == _target_type(target)
    assert TargetType.dataclass == _target_type(Target)


def test_handle_field_none(this_injector):
    class Unknown:
        pass

    assert None is this_injector(Unknown)


def test_handle_field_container(this_injector):
    # E.g. (c: ServiceContainer)
    field_type = this_injector.handle_field(ServiceContainer)
    assert ServiceContainer is field_type.__class__


def test_function_no_args(this_injector):
    """ The callable has no arguments """

    def dummy_service():
        return 99

    result = this_injector(target=dummy_service)
    assert 99 == result


def test_container_by_name(this_injector):
    """ The callable wants the container, but doesn't use type hints """

    def dummy_service(container):
        return 99

    result = this_injector(target=dummy_service)
    assert 99 == result


def test_container_by_type(this_injector):
    """ The callable wants the container, not by name, but type """

    def dummy_service(c: ServiceContainer):
        return 99

    result = this_injector(target=dummy_service)
    assert 99 == result


def test_handle_field_injected_servicecontainer(this_injector):
    def dummy_service(c: Injected[ServiceContainer]):
        return 99

    result = this_injector(target=dummy_service)
    assert 99 == result


def test_handle_field_injected_customer(this_container, this_injector):
    class Customer:
        pass

    this_container.register_singleton(Customer(), Customer)

    def dummy_service(customer: Injected[Customer]):
        return customer

    result = this_injector(target=dummy_service)
    assert Customer is result.__class__


def test_handle_field_injected_customer_experiment(this_container, this_injector, this_injector2):
    this_container.register_singleton(Customer(), Customer)

    InjectT = TypeVar('InjectT')

    def simple_factory(customer: Customer):
        return customer

    result = this_injector(target=simple_factory)
    assert 'Base Customer' == result.name

    # ==============================================================
    # Let's start using Annotated so we can bring in the other
    # features from the current injector.
    def annotated_factory(customer: Annotated[Customer, _inject_marker]):
        return customer

    result = this_injector(target=annotated_factory)
    assert 'Base Customer' == result.name

    # ==============================================================
    # The current injector lets the return type be different than
    # the lookup type. We want the result to be FrenchCustomer,
    # but ask the injector for the registered Customer.

    def frenchcustomer_factory(customer: Annotated[FrenchCustomer, Customer, _inject_marker]):
        # The injector looked up "Customer" which
        return customer

    result = this_injector2(target=frenchcustomer_factory)
    assert 'French Customer' == result.name

    # ==============================================================
    # The current injector also lets you pluck off just an
    # attribute, which is handy for building a props-based
    # component system.

    def attr_factory(customer_name: Annotated[str, Customer, Attr('name'), _inject_marker]):
        # The injector looked up "Customer" which
        return f'Name: {customer_name}'

    result = this_injector2(target=attr_factory)
    assert 'Name: French Customer' == result

    # ==============================================================
    # That's getting a little noisy. Would be nice to use a TypeAlias
    # to at least cut down that last part. But the alias fails at
    # runtime with:
    #   TypeError: Too many parameters for typing.Annotated[~InjectT,
    #      <object object at 0x10a4ce8c0>]; actual 3, expected 1
    #
    # mypy fails with:
    # tests/test_593_injector.py:177: error: Bad number of arguments for type alias, expected: 1, given: 3
    # tests/test_593_injector.py:177: error: Invalid type comment or annotation
    # tests/test_593_injector.py:177: note: Suggestion: use Attr[...] instead of Attr(...)

    Injected = Annotated[InjectT, _inject_marker]

    def injected_factory(customer_name: Injected[str, Customer, Attr('name')]):
        # The injector looked up "Customer" which
        return f'Name: {customer_name}'

    result = this_injector2(target=injected_factory)
    assert 'Name: French Customer' == result
