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
    c = r.create_container()
    return c
