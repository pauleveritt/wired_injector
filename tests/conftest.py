import pytest
from wired import ServiceContainer, ServiceRegistry


class Customer:
    name: str

    def __init__(self):
        self.name = 'Some Customer'


class FrenchCustomer(Customer):
    name: str

    def __init__(self):
        super().__init__()
        self.name = 'French Customer'


@pytest.fixture
def this_container() -> ServiceContainer:
    r = ServiceRegistry()
    r.register_singleton(Customer(), Customer)
    french_customer = FrenchCustomer()
    r.register_singleton(french_customer, FrenchCustomer)
    c = r.create_container()
    return c


@pytest.fixture
def context_container() -> ServiceContainer:
    r = ServiceRegistry()
    customer = Customer()
    r.register_singleton(customer, Customer)
    french_customer = FrenchCustomer()
    r.register_singleton(french_customer, FrenchCustomer)
    c = r.create_container(context=french_customer)
    return c
