from dataclasses import dataclass
from typing import Optional

from wired import service_factory
from wired_injector import injectable
from wired_injector.operators import Get

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore


# Normal kind of customer
@dataclass
class Customer:
    name: Optional[str] = 'Customer'


# Default View
@service_factory()
@dataclass
class View:
    name: Optional[str] = 'View'

    def __call__(self):
        return self.name

    @property
    def caps_name(self):
        return self.name.upper()

    @classmethod
    def __wired_factory__(cls, container):
        return cls()


# Example of an injectable factory
@injectable()
@dataclass
class Greeting:
    customer_name: Annotated[str, Get(View, attr='caps_name')]

    def __call__(self):
        return f'Hello {self.customer_name}'


# Special kind of Customer
@dataclass
class FrenchCustomer(Customer):
    name: Optional[str] = 'French Customer'


# Special kind of View, for that special kind of Customer
@service_factory(for_=View, context=FrenchCustomer)
@dataclass
class FrenchView(View):
    name: Optional[str] = 'French View'

    @classmethod
    def __wired_factory__(cls, container):
        return cls()
